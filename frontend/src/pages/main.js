import { useState, useEffect } from "react"
import { Button, Form, Input, Select, message} from 'antd'
import {api} from '../../src/api/api'
function Main() {

    const onFinish = async (values) => {
        const res = await api.post('/speech/',{word:values})
        console.log(res.data);
    }

    return (
        <div>
            <h1>test</h1>
            <Form
                onFinish={onFinish}
            >
                <Form.Item name="text">
                    <Input></Input>
                </Form.Item>

                <Form.Item style={{display: 'inline-flex',marginLeft:'15px', }}>
                    <Button type="primary" htmlType="submit" style={{width:200, borderRadius: 20, backgroundColor: '#3CB371', font:'bold'}}>
                        Generate
                    </Button>
                </Form.Item>
            </Form>

        </div>
    )
}

export default Main 