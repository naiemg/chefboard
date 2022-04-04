import React from "react";
import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { MENU_ITEM_API_ENDPOINT } from "./config";

import { DataGrid } from "@mui/x-data-grid";
import { Button, Snackbar } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";

const useFakeMutation = () => {
  return React.useCallback(
    (item) =>
      new Promise((resolve, reject) =>
        setTimeout(() => {
          resolve({ ...item });
        }, 200)
      ),
    []
  );
};

function MenuItemsApplication() {
  const category_id = JSON.parse(
    document.getElementById("category_id").textContent
  );

  const [menuItems, setMenuItems] = useState([]);
  const [selectionModel, setSelectionModel] = useState({});

  const mutateRow = useFakeMutation();
  const [snackbar, setSnackbar] = React.useState(null);

  const handleCloseSnackbar = () => setSnackbar(null);

  const processRowUpdate = React.useCallback(
    async (newRow) => {
      try {
        // Make the HTTP request to save in the backend
        const response = await mutateRow(newRow);
        setSnackbar({
          children: "Item successfully saved",
          severity: "success",
        });

        // update the row in the database using axios put method
        await axios.put(`${MENU_ITEM_API_ENDPOINT}/${response.id}/`, response, {
          headers: {
            Authorization: `Token ${process.env.API_KEY}`,
          },
        });

        return response;
      } catch (error) {
        setSnackbar({ children: "Error while saving item", severity: "error" });
        throw error; // Throw again the error to reject the promise and keep the cell in edit mode
      }
    },
    [mutateRow]
  );

  const handleDelete = () => {
    if (selectionModel.length === 0) {
      setSnackbar({
        children: "Please select an item to delete",
        severity: "warning",
      });
      return;
    }

    for (let i = 0; i < selectionModel.length; i++) {
      axios
        .delete(`${MENU_ITEM_API_ENDPOINT}/${selectionModel[i]}/`, {
          headers: {
            Authorization: `Token ${process.env.API_KEY}`,
          },
        })
        .then(() => {
          setSnackbar({
            children: `${selectionModel.length} Items successfully deleted`,
            severity: "success",
          });
        })
        .catch((error) => {
          setSnackbar({
            children: "Error while deleting item",
            severity: "error",
          });
        });
    }
    setSelectionModel({});
    fetchMenuItems();
  };

  const fetchMenuItems = () => {
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

  const postMenuItem = (data, form) => {
    axios
      .post(`${MENU_ITEM_API_ENDPOINT}/`, data, {
        headers: {
          Authorization: `Token ${process.env.API_KEY}`,
        },
      })
      .then((response) => {
        setSnackbar({
          children: "Item successfully added",
          severity: "success",
        });

        form.reset();
        form.elements[0].focus();
        fetchMenuItems();
      })
      .catch((error) => {
        setSnackbar({
          children: `Error while saving item! ${error}`,
          severity: "error",
        });
      });
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    const form = event.target;

    const data = {
      item_name: form.name.value,
      price: form.price.value,
      category: JSON.parse(document.getElementById("category_id").textContent),
      is_active: true,
    };

    postMenuItem(data, form);
  };

  const data = useMemo(() => [...menuItems], [menuItems]);

  const columns = useMemo(
    () =>
      menuItems[0]
        ? Object.keys(menuItems[0]).map((key) => {
            return {
              field: key,
              headerName: key,
              width: "200",
              type: typeof menuItems[0][key],
              editable: key === "id" || key == "category" ? false : true,
            };
          })
        : [],
    [menuItems]
  );

  useEffect(() => {
    fetchMenuItems();
  }, []);

  return (
    <>
      <Box
        component="form"
        sx={{
          "& > :not(style)": { m: 1, width: "25ch" },
        }}
        noValidate
        autoComplete="off"
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <TextField id="name" label="Item Name" variant="outlined" autoFocus />
        <TextField id="price" label="Price" variant="outlined" type="decimal" />
        <Button color="primary" variant="contained" type="submit">
          Add Item
        </Button>
      </Box>

      <div style={{ width: "100%" }}>
        <DataGrid
          autoHeight
          editMode="row"
          rows={data}
          columns={columns}
          checkboxSelection
          onSelectionModelChange={(newSelectionModel) => {
            setSelectionModel(newSelectionModel);
          }}
          selectionModel={selectionModel}
          density="compact"
          processRowUpdate={processRowUpdate}
          experimentalFeatures={{ newEditingApi: true }}
        />

        {!!snackbar && (
          <Snackbar
            open
            anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
            onClose={handleCloseSnackbar}
            autoHideDuration={6000}
          >
            <Alert {...snackbar} onClose={handleCloseSnackbar} />
          </Snackbar>
        )}

        <Button color="secondary" onClick={handleDelete}>
          Delete Selected Items
        </Button>
      </div>
    </>
  );
}

export default MenuItemsApplication;
