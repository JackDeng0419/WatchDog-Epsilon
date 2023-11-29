// src/views/home.js
import React from 'react';
import { View, Button } from 'react-native';
import { Card } from '@rneui/base';
import { StyleSheet } from 'react-native';

import AppHeader from '../components/header';

const Home = ({ navigation }) => {
  const styles = StyleSheet.create({
    highlight: {
      fontWeight: '700',
    },
  });

  return (
    <View style={styles.container}>
      <AppHeader navigation={navigation} />

      <Card containerStyle={styles.card}>
        <View>
          <Button
            title="Patient List"
            onPress={() => navigation.navigate('PatientList')}
            containerStyle={styles.buttonContainer}
          />
        </View>
      </Card>

      <Card containerStyle={styles.card}>
        <View>
          <Button
            title="Create Patient"
            onPress={() => navigation.navigate('CreatePatient')}
            containerStyle={styles.buttonContainer}
          />
        </View>
      </Card>

      <Card containerStyle={styles.card}>
        <View>
          <Button
            title="Notification List"
            onPress={() => navigation.navigate('NotificationList')}
            containerStyle={styles.buttonContainer}
          />
        </View>
      </Card>
    </View>
  );
};


export default Home;
