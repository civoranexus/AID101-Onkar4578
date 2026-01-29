import FarmerForm from "./components/FarmerForm";
import FarmerList from "./components/FarmerList";
import YieldPrediction from "./components/YieldPrediction";
import IrrigationAdvice from "./components/IrrigationAdvice";

function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>AgriAssist AI Platform</h1>

      <FarmerForm />
      <FarmerList />
      <YieldPrediction />
      <IrrigationAdvice />
    </div>
  );
}

export default App;
