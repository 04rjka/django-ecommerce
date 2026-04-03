import { useState,useEffect } from "react";
import axios from "axios";

export default function useFetch(url){
    const [data, setData] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(()=>{
        axios.get(url)
        .then((res)=>{ setData(res.data) })
        .catch(()=> { setError("Error Occured") })
        .finally(()=>{ setLoading(false) })
    },[url])

    return { data, loading , error }
}