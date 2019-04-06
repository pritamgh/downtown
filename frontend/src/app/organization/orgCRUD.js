import axios from 'axios';
const API_URL = 'http://localhost:8000/api/v1/organization';

export default class Organization{

    getOrganizationList() {
        const url = `${API_URL}/list/`;
        return axios.get(url).then(response => response.data)
                .catch(error => alert(error));
    }

    createOrganization(organization) {
        console.log(organization);
        const url = `${API_URL}/create/`;
        const config = {
            headers: {
                'content-type': 'multipart/form-data',
                'Accept': '*/*', 
                'Accept-Encoding': 'gzip, deflate'
            }
        }
        return axios.post(url, organization, config)
    }
}
