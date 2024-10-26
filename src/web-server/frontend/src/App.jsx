// import route related functions
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

// import pages
import Chat from './pages/Chat';
import Error from './pages/Error'

const AppContent = () => {

  return (
    <Routes>
      <Route path="/chat/" element={<Error error="Agent not specified"/>} />
      <Route path="/chat/:agent" element={<Chat />} />
      <Route path="*" element={<Error error="Invalid request"/>} />
    </Routes>
  )
}


const App = () => {
  return (
      <Router>
        <AppContent />
      </Router>
  )
}

export default App
