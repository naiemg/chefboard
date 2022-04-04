import React from "react";
import axios from "axios";
import { MENU_ITEM_API_ENDPOINT } from "./config";

function NewItem() {
  const handleSubmit = (event) => {
    event.preventDefault();

    const form = event.target;

    const data = {
      item_name: form.name.value,
      price: form.price.value,
      category: JSON.parse(document.getElementById("category_id").textContent),
      is_active: true,
    };

    axios
      .post(`${MENU_ITEM_API_ENDPOINT}/`, data, {
        headers: {
          Authorization: `Token ${process.env.API_KEY}`,
        },
      })
      .then((response) => {
        console.log(response);
        form.reset();
      })
      .catch((error) => {
        console.log(error);
      });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Name</label>
          <input
            type="text"
            className="form-control"
            id="name"
            placeholder="Enter name"
          />
        </div>

        <div className="form-group">
          <label htmlFor="price">Price</label>
          <input
            type="decimal"
            className="form-control"
            id="price"
            placeholder="Enter price"
          />
        </div>

        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>
    </div>
  );
}

export default NewItem;
