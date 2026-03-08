import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import ProjectBrief from './pages/ProjectBrief'
import GenerationProgress from './pages/GenerationProgress'
import FileTree from './pages/FileTree'
import BuildConsole from './pages/BuildConsole'
import PlatformPackages from './pages/PlatformPackages'
import LearningStore from './pages/LearningStore'
import Header from './components/Header'
import Sidebar from './components/Sidebar'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Header />
        <div className="app-body">
          <Sidebar />
          <main className="content">
            <Routes>
              <Route path="/" element={<ProjectBrief />} />
              <Route path="/generation/:projectId" element={<GenerationProgress />} />
              <Route path="/files/:projectId" element={<FileTree />} />
              <Route path="/build/:projectId" element={<BuildConsole />} />
              <Route path="/packages/:projectId" element={<PlatformPackages />} />
              <Route path="/learning-store" element={<LearningStore />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App
