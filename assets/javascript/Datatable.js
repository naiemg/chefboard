import React from "react";
import { DataGrid } from "@mui/x-data-grid";
import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import { Snackbar } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import { MENU_ITEM_API_ENDPOINT } from "./config";

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

function Datatable() {
  const category_id = JSON.parse(
    document.getElementById("category_id").textContent
  );

  const [menuItems, setMenuItems] = useState([]);

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
    <div style={{ height: "300px", width: "100%" }}>
      <DataGrid
        editMode="row"
        rows={data}
        columns={columns}
        pageSize={10}
        checkboxSelection
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
    </div>
  );
}

export default Datatable;
