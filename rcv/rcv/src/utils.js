export default {
    // Function for retrieving cookie values
    getCookie: function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    // Function for building HTTP requests
    _sendRequest: function _sendRequest(method, url, data) {
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', this.getCookie('csrftoken'));
        formData.append('json', JSON.stringify(data));
        let requestData = {
            'method': method,
            'credentials': 'same-origin',
            'body': formData,
        }
        return fetch(url, requestData);
    },

    // Helper function for GET requests
    get: function get(url, /* data */) {
        // TODO: Parse Data
        return this._sendRequest('GET', url)
    },

    // Helper function for POST requests
    post: function post(url, data) {
        return this._sendRequest('POST', url, data)
    },
}