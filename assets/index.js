import React from "react";
import ReactDOM from "react-dom/client";
import MenuItemsApplication from "./javascript/MenuItemsApplication";
import ScreenDesignTool from "./javascript/ScreenDesignTool";

if (document.getElementById("screen_design_tool")) {
  const root = ReactDOM.createRoot(
    document.getElementById("screen_design_tool")
  );
  root.render(<ScreenDesignTool />);
} else if (document.getElementById("data_table")) {
  const root = ReactDOM.createRoot(document.getElementById("data_table"));
  root.render(<MenuItemsApplication />);
}
