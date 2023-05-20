import {HashRouter, Route, Routes} from 'react-router-dom'
import English from './pages/english'
import Chinese from './pages/chinese'
import English2 from './pages/english2'
import Chinese2 from './pages/chinese2'
import Start from './pages/start';
import Test from './pages/test'

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
    <HashRouter>
      <Routes>
          <Route path="" element = {<Start/>}/>
          <Route path="english" element = {<English/>}/>
          <Route path="chinese" element = {<Chinese/>}/>
          <Route path="english2" element = {<English2/>}/>
          <Route path="chinese2" element = {<Chinese2/>}/>
          <Route path="test" element = {<Test/>}/>
      </Routes>
    </HashRouter>
  )
}

export default App;