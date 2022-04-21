import axios from "axios";
import React, { useEffect, useState } from "react";
import { MENU_ITEM_API_ENDPOINT } from "./config";

function CategoryBlock({ category }) {
  const [menu_items, setMenuItems] = useState(null);

  const Fetch_Menu_Items = (category_id) => {
    axios
      .get(`${MENU_ITEM_API_ENDPOINT}?category=${category_id}`, {
        headers: {
          Authorization: `Token ${process.env.API_KEY}`,
        },
      })
      .then((response) => {
        let fetched_items = response.data;
        setMenuItems(fetched_items);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    Fetch_Menu_Items(category.id);
  }, []);
  return (
    <div
      style={{
        margin: "10px",
        padding: "0.5rem",
        border: "1px solid black",
        borderRadius: "5px",
        backgroundColor: "lightgreen",
        fontSize: "1rem",
        lineHeight: "0.25rem",
      }}
    >
      <h5
        style={{
          margin: "0",
          padding: "0.5rem",
          fontSize: "1.5rem",
          fontWeight: "bold",
          textAlign: "center",
        }}
      >
        {category.name}
      </h5>
      {menu_items &&
        menu_items.map((menu_item) => {
          return (
            <div>
              <p>
                <b>{menu_item.item_name}</b> | {menu_item.price}
              </p>
            </div>
          );
        })}
    </div>
  );
}

export default CategoryBlock;
