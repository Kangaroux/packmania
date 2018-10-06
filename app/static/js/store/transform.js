export default {
  /* Gets the form and field errors from an API response */
  form(err) {
    const data = err.response.data;

    // If no status was included something is wrong with the server
    if(data.status == null) {
      return {
        formError: "An unexpected error occurred.",
        fieldErrors: {}
      };
    }

    return {
      formError: data.msg,
      fieldErrors: data.fields || {}
    };
  },

  /* Normalizes date fields to a Date object */
  dates(obj) {
    let newObj = Object.assign({}, obj);

    if(newObj.date_created)
      newObj.date_created = new Date(newObj.date_created);

    if(newObj.date_updated)
      newObj.date_updated = new Date(newObj.date_updated);

    if(newObj.date_joined)
      newObj.date_joined = new Date(newObj.date_joined);

    return newObj;
  },

  /* Normalizes a user returned from the API */
  user(obj) {
    return this.dates(obj);
  }
};