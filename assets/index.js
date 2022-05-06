import React from "react";
import ReactDOM from "react-dom/client";
import App from "./javascript/App";
import MenuItemsApplication from "./javascript/MenuItemsApplication";
import ScreenDesignTool from "./javascript/ScreenDesignTool";

if (document.getElementById("screen_design_tool")) {
  const root = ReactDOM.createRoot(
    document.getElementById("screen_design_tool")
  );
  root.render(
    <>
      <App />
      {/* <ScreenDesignTool /> */}
    </>
  );
} else if (document.getElementById("data_table")) {
  const root = ReactDOM.createRoot(document.getElementById("data_table"));
  root.render(<MenuItemsApplication />);
}
