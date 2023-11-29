// src/routes.js
import Login from './views/login';
import Home from './views/home';
import PatientList from './views/patient-list';
import UserProfile from './views/user-profile';
import PatientProfile from './views/patient-profile';
import CreatePatient from './views/create-patient';
import Notification from './views/notification';
import NotificationList from './views/notification-list';
import VideoPage from './views/video';


export const Routes = [
  { name: 'Home', component: Home },
  { name: 'PatientProfile', component: PatientProfile, initialParams: { patientId: null } },
  { name: 'CreatePatient', component: CreatePatient },
  { name: 'UserProfile', component: UserProfile },
  { name: 'PatientList', component: PatientList },
  { name: 'Notification', component: Notification, initialParams: { notificationId: null }  },
  { name: 'NotificationList', component: NotificationList },
  { name: 'VideoPage', component: VideoPage, initialParams: { videoId: null }  },
];

export { Login };
