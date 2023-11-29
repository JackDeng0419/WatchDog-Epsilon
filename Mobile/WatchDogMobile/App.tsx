/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React, { useEffect, useRef, useState } from 'react';
import { DeviceEventEmitter } from 'react-native';
import { NavigationContainer, NavigationContainerRef } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { Routes, Login } from './src/routes';
import { OneSignalApi, sendRequestToServer } from './src/apis/oneSignal-api';
import { Auth } from './src/components/auth';
import Alert from './src/components/alert';

const Stack = createNativeStackNavigator();

function App(): JSX.Element {
  const navigationRef = useRef<NavigationContainerRef<any>>(null);

  const [isAlertVisible, setIsAlertVisible] = useState(false);
  const [alertConfig, setAlertConfig] = useState({
    title: '',
    body: '',
    positiveButton: undefined,
    negativeButton: undefined
  });

  const [userToken, setUserToken] = useState<string | null>(null);
  const logIn = (token: string) => {
    setUserToken(token);
  }
  const logOut = () => {
    setUserToken(null);
  }
  const authContextValue = {
    userToken,
    setUserToken,
    logIn,
    logOut,
  };

  useEffect(() => {
    sendRequestToServer();

    const navigateToNotificationListener = DeviceEventEmitter.addListener(
      'navigateToScreen',
      (notification) => {
        if (!userToken && notification.targetScreen !== "Login") {
          navigationRef.current?.navigate("Login");
          return;
        }

        if (userToken && notification.targetScreen === "Login") {
          navigationRef.current?.navigate("Home");
          return;
        }

        navigationRef.current?.navigate(notification.targetScreen, { notificationId: notification.notificationId });
      }
    );

    const showAlertListener = DeviceEventEmitter.addListener(
      'showAlert',
      (config) => {
        setAlertConfig(config);
        setIsAlertVisible(true);
      }
    );

    return () => {
      navigateToNotificationListener.remove();
      showAlertListener.remove();
    };
  }, [userToken]);

  return (
    <Auth.Provider value={authContextValue}>
      <NavigationContainer
        ref={navigationRef}
        onStateChange={(state) => {
          // Check if state exists
          if (state) {
            const currentRouteName = state.routes[state.index]?.name;

            if (!userToken && currentRouteName !== "Login") {
              navigationRef.current?.navigate("Login");
              return;
            }

            if (userToken && currentRouteName === "Login") {
              navigationRef.current?.navigate("Home");
              return;
            }
          }
        }}
      >
        <OneSignalApi />
        <Stack.Navigator initialRouteName={userToken ? 'Home' : 'Login'} screenOptions={{ headerShown: false }}>
          <Stack.Screen name="Login" component={Login} />
          {Routes.map(route => (
            <Stack.Screen
              key={route.name}
              name={route.name}
              component={route.component}
              initialParams={route.initialParams}
            />
          ))}
        </Stack.Navigator>
        <Alert
          isVisible={isAlertVisible}
          title={alertConfig.title}
          body={alertConfig.body}
          positiveButton={alertConfig.positiveButton}
          negativeButton={alertConfig.negativeButton}
        />
      </NavigationContainer>
    </Auth.Provider>
  );
}

export default App;