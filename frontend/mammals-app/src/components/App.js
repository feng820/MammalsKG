import {
  BrowserRouter as Router,

  Route, Switch
} from "react-router-dom";
import { Ecoregion } from './Ecoregion';
import { Main } from './Main';
import { MammalDetail } from './MammalDetail';
import { SubspeciesMap } from './SubspeciesMap';
import { TopNavBar } from './TopNavBar';


function App() {
  return (
    <Router>
      <div className="App">
        <TopNavBar /> 
        <Switch>
            <Route exact path="/mammal/:mammalId" render={(props) => (
                <MammalDetail key={props.match.params.mammalId} {...props} />
              )}
            />
            <Route path="/mammal/:mammalId/map" component={SubspeciesMap} />
            <Route path="/ecoregion/:ecoId" component={Ecoregion} />
            <Route exact path="/" component={Main} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
