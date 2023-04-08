import { useState, useEffect } from "react"
import { Button, Form, Input, Select, message} from 'antd'
import axios from 'axios'

function Main() {

    return (
        <div>
            <h1>test</h1>
            <Button type="primary" htmlType="submit" style={{width:200, borderRadius: 20, backgroundColor: '#3CB371', font:'bold'}}>
                                Generate</Button>
        </div>
    )
}

export default Main 