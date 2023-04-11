import Texty from 'rc-texty'
import QueueAnim from 'rc-queue-anim'
import { useNavigate } from 'react-router-dom'
import '../css/start.css'
function Start() {
    const nagative = useNavigate()

    const handleclick1 = ()=> {
        nagative('/english')
    }
    const handleclick2 = ()=> {
        nagative('/chinese')
    }
    return (
        <div className='main'>
            <div className='title'>
                <Texty>Simultaneous Interpretation</Texty>
            </div>
            <QueueAnim delay={600} className="queue-simple">
                <div key="a" className='button1-content'><button className='button1' onClick={handleclick1}>English to Chinese</button></div>
                <div key="b" className='button2-content'><button className='button2' onClick={handleclick2}>中 译 英</button></div>
            </QueueAnim>
        </div>


    )
}

export default Start