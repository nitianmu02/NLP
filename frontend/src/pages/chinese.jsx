import React, { useState, useEffect} from "react"
import { useNavigate } from "react-router-dom"
import '../css/main.css'

function Chinese() {
    const navigate = useNavigate()
    const [spokenText, setSpokenText] = useState('')
    const [interimTranscript, setInterimTranscript] = useState('')
    const [translatedText, setTranslatedText] = useState('')
    const [audioData, setAudioData] = useState(null)
    const [buttonVisible, setButtonVisible] = useState(false)

    const handleClick = () => {
        setButtonVisible(true)
    }

    const sendSpeechToBackend = (speechData) => {
        const socket = new WebSocket('ws://localhost:8000/ws/chinese/')
        socket.onopen = () => {
            console.log('WebSocket connection established')
            socket.send(JSON.stringify({ words: speechData }))
        }
        socket.onmessage = (event) => {
            const res = JSON.parse(event.data)
            console.log('res:', res)
            setTranslatedText(res.message)
            setAudioData(res.audio)
            socket.close()
        }
    }
    const playAudio = () => {
        if (audioData) {
            const audioBlob = base64ToBlob(audioData, 'audio/mpeg')
            const audioUrl = URL.createObjectURL(audioBlob)
            const audio = new Audio(audioUrl)
            audio.play()
        }
    }
    const base64ToBlob = (base64Data, contentType) => {
        const byteCharacters = atob(base64Data)
        const byteArrays = []
        for (let i = 0; i < byteCharacters.length; i++) {
            byteArrays.push(byteCharacters.charCodeAt(i))
        }
        const byteArray = new Uint8Array(byteArrays)
        return new Blob([byteArray], { type: contentType })
    }

    useEffect(() => {
        const recognition = new window.webkitSpeechRecognition()
        recognition.continuous = true
        recognition.interimResults = true
        recognition.lang = 'zh-CN'

        recognition.onresult = (event) => {
            let interimTranscript = ''
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    setSpokenText(event.results[i][0].transcript)
                } else {
                    interimTranscript += event.results[i][0].transcript + ' '
                }
            }
            setInterimTranscript(interimTranscript)
        }

        recognition.onend = () => {
            recognition.start()
        }

        recognition.start()

        return () => {
            recognition.stop()
        }
    }, [])

    useEffect(() => {
        sendSpeechToBackend(spokenText)
    }, [spokenText])

    useEffect(() => {
        
        playAudio()
        // eslint-disable-next-line
    }, [audioData])

    const handleclick = () => {
        navigate('/english/')
        window.location.reload()
    }

    return (
        <div className="main">
            {!buttonVisible && <button className="btn2" onClick={handleClick}>Let's start</button>}
            {buttonVisible && <section className="main-content">
                <div className="title">文本：</div>
                <div className="spoken">{spokenText}</div>
                <div className="interim">{interimTranscript !== '' ? interimTranscript : '用中文说点什么...'}</div>
                <div className="title2">翻译：</div>
                <div className="translate">{translatedText}</div>
                <button className="btn" onClick={handleclick}>英 译 中</button>
            </section>}
            
        </div>
    )
}

export default Chinese
