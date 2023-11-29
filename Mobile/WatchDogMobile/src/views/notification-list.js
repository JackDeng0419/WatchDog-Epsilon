// src/views/notification-list.js
import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Text, ScrollView, TouchableOpacity } from 'react-native';
import { Card } from '@rneui/base';

import { SUCCESS_STATUS, getNotificationsList } from '../apis/serve-api';
import AppHeader from '../components/header';
import { getStateColor } from '../components/state';

import { notificationStyles as styles } from '../asset/notification-list-style';

const NotificationList = ({ navigation }) => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchNotifications = async () => {
      const data = await getNotificationsList();
      if (data && data.status === SUCCESS_STATUS) {
        setNotifications(data.data.data);
      }
    };

    fetchNotifications();
  }, []);

  return (
    <View style={styles.container}>
      <AppHeader navigation={navigation} />

      <ScrollView>
        {notifications && notifications.length > 0 ? (
          notifications.map((notification, index) => (
            <TouchableOpacity
              key={index}
              onPress={() =>
                navigation.navigate('Notification', { notificationId: notification.notificationId })
              }
            >
              <Card containerStyle={styles.card}>
                <Card.Title>{notification.head}</Card.Title>
                <Card.Divider />

                <View style={styles.infoRow}>
                  <Text style={styles.label}>State:</Text>
                  <Text style={[styles.state, {color: getStateColor(notification.state)}]}>{notification.state}</Text>
                </View>
              </Card>
            </TouchableOpacity>
          ))
        ) : (
          <Text>No notifications available.</Text>
        )}
      </ScrollView>
    </View>
  );
};

export default NotificationList;