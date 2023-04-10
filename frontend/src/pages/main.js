import { useState, useEffect } from "react"
// import { Button, Form, Input, Select, message} from 'antd'
import {api} from '../../src/api/api'
function Main() {
    const [spokenText, setSpokenText] = useState('')
    const [interimTranscript, setInterimTranscript] = useState('')
    const [translatedText, setTranslatedText] = useState('');
    const recognition = new window.webkitSpeechRecognition()

    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'zh-CN';

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
            const newSpokenText = event.results[i][0].transcript;
            setSpokenText((prevSpokenTexts) => [...prevSpokenTexts, ' ', newSpokenText]);
          } else {
            interimTranscript += event.results[i][0].transcript + ''
          }
        }
        setInterimTranscript(interimTranscript)
    };

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

    return (
        <div>
            <h1>test</h1>
            <div style={{ fontSize: '24px'}}>{spokenText} </div>
            <div style={{ fontSize: '18px'}}>{interimTranscript}</div>
            <div style={{ fontSize: '24px' }}>translate：{translatedText}</div>
        </div>
    )
}

export default Main 