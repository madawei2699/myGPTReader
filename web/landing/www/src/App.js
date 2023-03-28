import './App.css';
import Header from './components/Header';
import { BrowserRouter as Router } from "react-router-dom";
import Hero from './components/Hero';
import Features from './components/Features';
import Pricing from './components/Pricing';

function App() {
  return (
    <Router basename='/'>
      <Header />
      <Hero />
      <Features />
      <Pricing />
    </Router>
  );
}

export default App;
