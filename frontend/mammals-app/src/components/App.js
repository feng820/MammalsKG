import { Main } from './Main';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import { TopNavBar } from './TopNavBar';
import { MammalDetail } from './MammalDetail';

function App() {
  return (
    <Router>
      <div className="App">
        <TopNavBar /> 
        <Switch>
            <Route exact path="/" component={Main} />
            <Route path="/mammal/:mammalId" component={MammalDetail} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
