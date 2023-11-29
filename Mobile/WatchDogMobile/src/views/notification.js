// src/views/notification.js
import React, { useState, useEffect } from 'react';
import { View, Text, Button } from 'react-native';

import { SUCCESS_STATUS, getNotificationById, updateNotification, getToken } from '../apis/serve-api';
import AppHeader from '../components/header';
import { getStateColor, NotificationState, ActionType } from '../components/state';
import Alert from '../components/alert';

import { notificationStyles as styles } from '../asset/notification-styles';

const Notification = ({ route, navigation }) => {
  const { notificationId } = route.params;
  const [notification, setNotification] = useState({
    state: NotificationState.DONE
  });
  const initialAlertState = {
    isVisible: false,
    title: 'Error',
    body: '',
    positiveButton: {
      text: 'OK',
      backgroundColor: 'grey',
      onPress: () => setAlert(prevState => ({ ...prevState, isVisible: false }))
    }
  };

  const [alert, setAlert] = useState(initialAlertState);

  const handleUpdateNotificationState = async (currentNotificationState) => {
    try {
      const response = await updateNotification({
        notification_id: notificationId,
        user_token: getToken(),
        state: currentNotificationState
      });

      if (response.status === SUCCESS_STATUS) {
        setNotification(prevNotification => ({ ...prevNotification, state: response.data.state }));
      } else {
        setAlert({
          ...initialAlertState,
          isVisible: true,
          body: response.data.message
        });
      }

    } catch (error) {
      setAlert({
        ...initialAlertState,
        isVisible: true,
        body: error.toString()
      });
    }
  };

  const getStatusButton = () => {
    switch (notification.state) {
      case NotificationState.UNDO:
        return (
          <Button
            title="Go to processing"
            color="green"
            onPress={() => {
              handleUpdateNotificationState(notification.state);
            }}
          />
        );
      case NotificationState.IN_PROCESS:
        return (
          <Button
            title="Processing completed"
            color="blue"
            onPress={() => {
              handleUpdateNotificationState(notification.state);
            }}
          />
        );
      case 'DONE':
        return (
          <Button
            title="Processed"
            color="gray"
            disabled
          />
        );
      default:
        return null;
    }
  };

  useEffect(() => {
    async function fetchNotificationDetails() {
      try {
        const data = await getNotificationById(notificationId);
        if (data && data.status === SUCCESS_STATUS) {
          setNotification(data.data.data);
        } else {
          setAlert({
            ...initialAlertState,
            isVisible: true,
            body: 'Failed to fetch notification details.'
          });
        }
      } catch (error) {
        setAlert({
          ...initialAlertState,
          isVisible: true,
          body: error.toString()
        });
      }
    }

    fetchNotificationDetails();
  }, [notificationId]);

  const renderNotificationDetails = () => {
    const renderContent = () => {
      if (notification.actionType === "LEAVEROOM") {
        return (
          <Text 
            style={styles.linkText}
            onPress={() => navigation.navigate("VideoPage", { videoId: notification.content })}
          >
            {notification.content}
          </Text>
        );
      } else {
        return <Text style={styles.infoText}>{notification.content}</Text>;
      }
    };

    if (!notification) {
      return <Text>Loading...</Text>;
    }

    return (
      <View>
        <Text style={styles.label}>Notification ID:</Text>
        <Text style={styles.infoText}>{notification.notificationId}</Text>
        <Text style={styles.label}>Head:</Text>
        <Text style={styles.infoText}>{notification.head}</Text>
        <Text style={styles.label}>Content:</Text>
        {renderContent()}
        <Text style={styles.label}>State:</Text>
        <Text style={[styles.infoText, { color: getStateColor(notification.state) }]}>{notification.state}</Text>
        <Text style={styles.label}>Action Type:</Text>
        <Text style={styles.infoText}>{notification.actionType}</Text>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <AppHeader navigation={navigation} />
      {renderNotificationDetails()}
      <View style={styles.buttonContainer}>
        {getStatusButton()}
      </View>

      <Alert 
        isVisible={alert.isVisible}
        title={alert.title}
        body={alert.body}
        positiveButton={alert.positiveButton}
      />
    </View>
  );
};

export default Notification;
