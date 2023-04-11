import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
// import { Button, Form, Input, Select, message} from 'antd'
import {api} from '../api/api'
import '../css/main.css'
function English() {
    const navigate = useNavigate()
    const [spokenText, setSpokenText] = useState('')
    const [interimTranscript, setInterimTranscript] = useState('')
    const [translatedText, setTranslatedText] = useState('');
    const recognition = new window.webkitSpeechRecognition()

    recognition.continuous = true;
    recognition.interimResults = true;

    const sendSpeechToBackend = async (speechData) => {
        if (speechData.trim() === '') {
            return
        }
        const res = await api.post('/speech/',{word:speechData})
        setTranslatedText(res.data)
        console.log('backend:' + res.data);
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
    }, [interimTranscript]);

    const handleclick = ()=> {
        navigate('/chinese/')
        window.location.reload();
    }

    return (
        <div className="main">
            <section className="main-content">
                <div className="title">Text:</div>
                <div className="spoken">{spokenText} </div>
                <div className="interim">{interimTranscript !== '' ? interimTranscript : 'Say something in English...'}</div>
                <div className="title2">Translate:</div>
                <div className="translate">{translatedText}</div>
                <button className="btn" onClick={handleclick}>Chinese to English</button>
            </section>
        </div>
    )
}

export default English 