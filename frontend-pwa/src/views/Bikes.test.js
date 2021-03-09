import { shallow, mount, render } from "enzyme";
import Bikes from "./Bikes";

it("renders without crashing", () => {
    shallow(<div className="content" />);
});

it("contains a map component", () => {
    const wrapper = render(<Bikes />);
    expect(wrapper.find('.leaflet-container')).toBeDefined();
});

// it("renders Account header", () => {
//     const wrapper = shallow(<App />);
//     const welcome = <h1>Display Active Users Account Details</h1>;
//     expect(wrapper.contains(welcome)).toEqual(true);
// });