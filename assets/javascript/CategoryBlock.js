import axios from "axios";
import React, { useEffect, useState } from "react";
import { MENU_ITEM_API_ENDPOINT } from "./config";

import { FormGroup, FormControlLabel, Checkbox } from "@material-ui/core";
import { Popper, Box } from "@material-ui/core";

function CategoryBlock({ category }) {
  const [menu_items, setMenuItems] = useState(null);

  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(anchorEl ? null : event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? "simple-popper" : undefined;

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
        backgroundColor: "lightgrey",
      }}
    >
      <FormGroup>
        <FormControlLabel
          aria-describedby={id}
          onMouseOver={handleClick}
          onMouseOut={handleClose}
          control={<Checkbox />}
          label={category.name}
        />
      </FormGroup>
      <Popper id={id} open={open} anchorEl={anchorEl} placement="right-end">
        <Box
          style={{
            padding: "0.5rem",
            border: "1px solid black",
            borderRadius: "5px",
            backgroundColor: "white",
          }}
          sx={{ border: 1, bgcolor: "background.paper" }}
        >
          <b>Includes:</b>
          {menu_items &&
            menu_items.map((menu_item) => {
              return (
                <ul
                  style={{
                    listStyle: "none",
                    padding: "0",
                    margin: "0",
                  }}
                >
                  <li>
                    {menu_item.item_name} — ${menu_item.price}
                  </li>
                </ul>
              );
            })}
        </Box>
      </Popper>
    </div>
  );
}

export default CategoryBlock;
