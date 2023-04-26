import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { api } from '../api/api'
import '../css/main.css'
function Chinese() {
    const navigate = useNavigate()
    const [spokenText, setSpokenText] = useState('')
    const [interimTranscript, setInterimTranscript] = useState('')
    const [translatedText, setTranslatedText] = useState('');
    const recognition = new window.webkitSpeechRecognition()

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'zh-CN';

    const sendSpeechToBackend = async (speechData) => {
        const words = speechData.trim().split(/([\u4E00-\u9FFF])/g).filter(word => word.trim() !== '')
        const res = await api.post('/speech/', { words: words })
        setTranslatedText(res.data)
        console.log('backend:' + res.data)
    }

    recognition.onresult = (event) => {
        let interimTranscript = ''
        for (let i = event.resultIndex; i < event.results.length; i++) {
            if (event.results[i].isFinal) {
                setSpokenText(event.results[i][0].transcript)
            } else {
                interimTranscript += event.results[i][0].transcript + ''
            }
        }
        setInterimTranscript(interimTranscript)
    }
    recognition.onend = () => {
        recognition.start()
    }

    useEffect(() => {
        recognition.start()
        // eslint-disable-next-line 
    }, [])

    useEffect(() => {
        if (interimTranscript.trim() !== '') {
            sendSpeechToBackend(interimTranscript.trim());
        }
    }, [interimTranscript])


    const handleclick = () => {
        navigate('/english/')
        window.location.reload()
    }
    return (
        <div className="main">
            <section className="main-content">
                <div className="title">文本：</div>
                <div className="spoken">{spokenText}</div>
                <div className="interim">{interimTranscript !== '' ? interimTranscript : '用中文说点什么...'}</div>
                <div className="title2">翻译：</div>
                <div className="translate">{translatedText}</div>
                <button className="btn" onClick={handleclick}>英 译 中</button>
            </section>
        </div>
    )
}

export default Chinese 