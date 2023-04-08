import {HashRouter, Route, Routes} from 'react-router-dom'
import Main from './pages/main';
function App() {
  return (
    <HashRouter>
      <Routes>
          <Route path="" element = {<Main/>}/>
      </Routes>
    </HashRouter>
  )
}

export default App;