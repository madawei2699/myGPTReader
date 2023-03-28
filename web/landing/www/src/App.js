import './App.css';
import Header from './components/Header';
import { BrowserRouter as Router } from "react-router-dom";
import Hero from './components/Hero';
import Features from './components/Features';
import Pricing from './components/Pricing';
import Footer from './components/Footer';

function App() {
  return (
    <Router basename='/'>
      <Header />
      <Hero />
      <Features />
      <Pricing />
      <Footer />
    </Router>
  );
}

export default App;
