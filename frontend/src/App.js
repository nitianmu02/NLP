import {HashRouter, Route, Routes} from 'react-router-dom'
import English from './pages/english'
import Chinese from './pages/chinese'
import Start from './pages/start';
import { BrowserRouter as Router, Switch } from "react-router-dom";
import Chat from "./Chat";
function App() {
  // return (
  //   <HashRouter>
  //     <Routes>
  //         <Route path="" element = {<Start/>}/>
  //         <Route path="english" element = {<English/>}/>
  //         <Route path="chinese" element = {<Chinese/>}/>
  //     </Routes>
  //   </HashRouter>
  // )
  return (
    <Routes>
        <Route path="/chat/:room_name" component={Chat} />
        {/* 其他路由 */}
    </Routes>
  );
}

export default App;