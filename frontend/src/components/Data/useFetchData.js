import { useState, useEffect } from 'react';
import axios from 'axios';

const useFetchData = (endpoint) => {
    const [data, setData] = useState(null);

    useEffect(() => {
        const validEndpoints = ['/events/', '/venues/'];

        if (!validEndpoints.includes(endpoint)) {
            console.error('Invalid endpoint:', endpoint);
            return;
        }

        axios.get(`http://localhost:8000/api${endpoint}`)
            .then(res => {
                setData(res.data);
            })
            .catch(err => {
                console.log(err);
            });
    }, [endpoint]);

    return data;
};

export default useFetchData;