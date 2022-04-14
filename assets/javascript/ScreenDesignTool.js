import axios from "axios";
import React, { useEffect, useState } from "react";
import { CATEGORY_ENDPOINT, MENU_ITEM_API_ENDPOINT } from "./config";

function ScreenDesignTool() {
  const restaurant_id = JSON.parse(
    document.getElementById("restaurant_id").textContent
  );
  const [categories, setCategories] = useState(null);
  const [hasFetchedCategories, setHasFetchedCategories] = useState(false);

  const Fetch_Categories = () => {
    axios
      .get(`${CATEGORY_ENDPOINT}?restaurant=${restaurant_id}`, {
        headers: {
          Authorization: `Token ${process.env.API_KEY}`,
        },
      })
      .then((response) => {
        let fetched_items = response.data;
        setCategories(fetched_items);

        setHasFetchedCategories(true);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const Fetch_Menu_Items = (category_id) => {
    axios
      .get(`${MENU_ITEM_API_ENDPOINT}?category=${category_id}`, {
        headers: {
          Authorization: `Token ${process.env.API_KEY}`,
        },
      })
      .then((response) => {
        let fetched_items = response.data;

        setCategories((prevState) => {
          let new_categories = [...prevState];
          new_categories.forEach((category) => {
            if (category.id === category_id) {
              category.menu_items = fetched_items;
            }
          });
          return new_categories;
        });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    if (hasFetchedCategories) {
      categories.forEach((category) => {
        Fetch_Menu_Items(category.id);
      });
    }
  }, [hasFetchedCategories]);

  useEffect(() => {
    Fetch_Categories();
  }, []);

  return (
    <>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          flexWrap: "wrap",
          height: `100vh`,
          width: `100vw`,
          backgroundColor: "#f5f5f5",
          fontSize: ".8em",
          lineHeight: "2em",
          padding: "1.5em",
        }}
      >
        {categories &&
          categories.map((category) => {
            return (
              <div key={category.id}>
                <h4>{category.name}</h4>
                <div>
                  {category.menu_items &&
                    category.menu_items.map((menu_item) => {
                      return (
                        <div key={menu_item.id}>
                          <span>
                            {menu_item.item_name} ... {menu_item.price}
                          </span>
                        </div>
                      );
                    })}
                </div>
              </div>
            );
          })}
      </div>
    </>
  );
}

export default ScreenDesignTool;
