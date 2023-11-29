// src/apis/serve-api.js
import axios from 'axios';

import { SERVER_END_POINT } from '../config';

export const SUCCESS_STATUS = 'success';
export const ERROR_STATUS = 'error';

let userToken = null;
export const setToken = (token) => {
  userToken = token;
};
export const getToken = () => userToken;

const axiosConfig = {
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': `Bearer ${getToken()}`
  },
  transformRequest: [
    (data) => {
      let formData = new URLSearchParams();
      for (let key in data) {
        formData.append(key, data[key]);
      }
      return formData.toString();
    },
  ],
};

const processRequest = async (name, requestFunc, ...params) => {
  try {
    const response = await requestFunc(...params);
    return response.data;
  } catch (error) {
    return {
      status: ERROR_STATUS,
      data: 'Unknown error at: ' + name
    };
  }
};

export const createNewPatient = (patientData) => {
  return processRequest(createNewPatient.name, axios.post, SERVER_END_POINT + 'patient/create/', patientData, axiosConfig);
};

export const getPatientsList = () => {
  return processRequest(getPatientsList.name, axios.get, SERVER_END_POINT + 'patient/list/');
};

export const getPatientById = (patientId) => {
  return processRequest(getPatientById.name, axios.get, SERVER_END_POINT + `patient/${patientId}/`);
};

export const getNotificationsList = () => {
  return processRequest(getNotificationsList.name, axios.get, SERVER_END_POINT + 'notification/list/');
};

export const getNotificationById = (notificationId) => {
  return processRequest(getNotificationById.name, axios.get, SERVER_END_POINT + `notification/${notificationId}/`);
};

export const updateNotification = (notificationData) => {
  return processRequest(updateNotification.name, axios.post, SERVER_END_POINT + 'notification/update/', notificationData, axiosConfig);
};

export const getVideoById = (videoId) => {
  return processRequest(getVideoById.name, axios.get, SERVER_END_POINT + `video/download/${videoId}/`);
};

export const loginUser = async (username, password) => {
  const response = await processRequest(loginUser.name, axios.post, SERVER_END_POINT + 'user/login/', { username, password }, axiosConfig);

  if (response.status === SUCCESS_STATUS && response.data.token) {
    setToken(response.data.token);
  }

  return response;
};

export const logoutUser = async () => {
  const response = await processRequest(logoutUser.name, axios.post, SERVER_END_POINT + 'user/logout/', { token: getToken() }, axiosConfig);
  if (response.status === SUCCESS_STATUS) {
    setToken(null);
  }
  return response;
};
