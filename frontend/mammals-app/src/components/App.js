import { Main } from './Main';
import {
  BrowserRouter as Router,
  Switch,
  Route,
} from "react-router-dom";

import { TopNavBar } from './TopNavBar';
import { MammalDetail } from './MammalDetail';
import { Ecoregion } from './Ecoregion';
import { SubspeciesMap } from './SubspeciesMap';

function App() {
  return (
    <Router>
      <div className="App">
        <TopNavBar /> 
        <Switch>
            <Route exact path="/mammal/:mammalId" render={(props) => (
              <MammalDetail key={props.match.params.mammalId} {...props} />)} />
            <Route path="/mammal/:mammalId/map" component={SubspeciesMap} />
            <Route path="/ecoregion/:ecoId" component={Ecoregion} />
            <Route exact path="/" component={Main} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
