import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"
import '../css/main.css'
function English2() {
    const navigate = useNavigate()
    const [spokenText, setSpokenText] = useState('')
    const [interimTranscript, setInterimTranscript] = useState('')
    const [translatedText, setTranslatedText] = useState('');

    const sendSpeechToBackend = async (speechData) => {
        const socket = new WebSocket('ws://localhost:8000/ws/result/');
        socket.onopen = () => {
            const words = speechData.trim().split(' ')
            console.log('WebSocket connection established');
            socket.send(JSON.stringify({ words: words }));
        };
        socket.onmessage = (event) => {
            const res = JSON.parse(event.data);
            console.log('res:', res);
            setTranslatedText(res.message);
            socket.close();
        };
    }

    useEffect(() => {
        const recognition = new window.webkitSpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onresult = (event) => {
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    setSpokenText(event.results[i][0].transcript);
                } else {
                    interimTranscript += event.results[i][0].transcript + ' ';
                }
            }
            setInterimTranscript(interimTranscript);
        };

        recognition.onend = () => {
            recognition.start();
        };

        recognition.start();

        return () => {
            recognition.stop();
        };
    }, []);

    useEffect(() => {
        if (interimTranscript.trim() !== '') {
            sendSpeechToBackend(interimTranscript.trim());
        }
    }, [interimTranscript])

    const handleclick = () => {
        navigate('/chinese2/')
        window.location.reload()
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

export default English2