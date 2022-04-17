import axios from "axios";
import React, { useEffect, useState } from "react";
import { CATEGORY_ENDPOINT, MENU_ITEM_API_ENDPOINT } from "./config";

import { Grid, Chip } from "@material-ui/core";

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
          backgroundColor: `#4158D0`,
          backgroundImage: `linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%)`,
          padding: "1rem",
          margin: "1rem",
          borderRadius: "1rem",
          color: "white",
          width: "100vw",
          height: "100vh",
        }}
      >
        <Grid container spacing={3}>
          {categories &&
            categories.map((category) => {
              return (
                <Grid item xs={12} sm={6} md={4} lg={2} key={category.id}>
                  <div key={category.id}>
                    <p
                      style={{
                        textDecoration: "underline",
                      }}
                    >
                      {category.name}
                    </p>
                    <div>
                      {category.menu_items &&
                        category.menu_items.map((menu_item) => {
                          return (
                            <Grid item lg={12} key={menu_item.id}>
                              <div key={menu_item.id}>
                                <Grid
                                  container
                                  spacing={1}
                                  justifyContent={"space-between"}
                                  style={{
                                    fontSize: "1.5rem",
                                  }}
                                >
                                  <Grid item key={menu_item.id}>
                                    {menu_item.item_name}
                                  </Grid>
                                  <Grid item key={menu_item.id}>
                                    <Chip
                                      variant="outlined"
                                      label={menu_item.price}
                                      style={{
                                        backgroundColor: "#4158D0",
                                        color: "white",
                                        border: "1px solid white",
                                      }}
                                    />
                                  </Grid>
                                </Grid>
                              </div>
                            </Grid>
                          );
                        })}
                    </div>
                  </div>
                </Grid>
              );
            })}
        </Grid>
      </div>
    </>
  );
}

export default ScreenDesignTool;
