import axios from "axios";
import React, { useEffect, useState } from "react";
import { CATEGORY_ENDPOINT, MENU_ITEM_API_ENDPOINT } from "./config";

import { Grid } from "@material-ui/core";
import CategoryBlock from "./CategoryBlock";

import { DragDropContext, Droppable, Draggable } from "react-beautiful-dnd";

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

  const handleOnDragEnd = (result) => {
    console.log(result);

    const items = Array.from(categories);
    const [reorderedItem] = items.splice(result.source.index, 1);
    items.splice(result.destination.index, 0, reorderedItem);

    setCategories(items);
  };

  return (
    <>
      <Grid container>
        <DragDropContext onDragEnd={handleOnDragEnd}>
          <Droppable droppableId="categories">
            {(provided) => (
              <div {...provided.droppableProps} ref={provided.innerRef}>
                {categories &&
                  categories.map((category, index) => {
                    return (
                      <Draggable
                        key={category.id}
                        draggableId={category.name}
                        index={index}
                      >
                        {(provided) => (
                          <div
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            ref={provided.innerRef}
                          >
                            <CategoryBlock
                              key={category.name}
                              category={category}
                            />
                          </div>
                        )}
                      </Draggable>
                    );
                  })}
                {provided.placeholder}
              </div>
            )}
          </Droppable>
        </DragDropContext>
      </Grid>
    </>
  );
}

export default ScreenDesignTool;
