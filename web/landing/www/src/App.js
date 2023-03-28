import './index.css';
import Header from './components/Header';
import { BrowserRouter as Router } from "react-router-dom";
import Hero from './components/Hero';

function App() {
  return (
    <Router basename='/'>
      <Header />
      <Hero />
    </Router>
  );
}

export default App;
