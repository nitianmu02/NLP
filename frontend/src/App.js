import {HashRouter, Route, Routes} from 'react-router-dom'
import English from './pages/english'
import Chinese from './pages/chinese'
import Start from './pages/start';

function App() {
  return (
    <HashRouter>
      <Routes>
          <Route path="" element = {<Start/>}/>
          <Route path="english" element = {<English/>}/>
          <Route path="chinese" element = {<Chinese/>}/>
      </Routes>
    </HashRouter>
  )
}

export default App;