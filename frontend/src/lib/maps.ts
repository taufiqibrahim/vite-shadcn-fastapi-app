import { ACCESS_TOKEN_KEY, API_BASE_URL } from "@/constants";


export const transformRequest = (url: any, resourceType: any) => {
    if (resourceType === 'Tile' && url.indexOf(API_BASE_URL) > -1) {
        const token = localStorage.getItem(ACCESS_TOKEN_KEY);
        return {
            url: url,
            headers: {'Authorization': `Bearer ${token}`},
            credentials: 'include'
        };
    }
}
