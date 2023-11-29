// src/views/patient-profile.js
import React, { useState, useEffect } from 'react';
import { View, Text, Switch } from 'react-native';
import { Card } from '@rneui/base';
import AppHeader from '../components/header';
import { useRoute } from '@react-navigation/native';

import { getPatientById } from '../apis/serve-api';

import { patientProfileStyles as styles } from '../asset/patient-profile-style';

const PatientProfile = ({ navigation }) => {
  const route = useRoute();
  const patientId = route.params.patientId;

  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [gender, setGender] = useState('');
  const [offBed, setOffBed] = useState(false);
  const [exitDoor, setExitDoor] = useState(false);

  useEffect(() => {
    const fetchPatientData = async () => {
      const patientData = await getPatientById(patientId);
      patient = patientData.patient
      if (patient) {
        setFirstName(patient.first_name);
        setLastName(patient.last_name);
        setGender(patient.gender);
      }
    };
    fetchPatientData();
  }, [patientId]);

  return (
    <View style={styles.container}>
      <AppHeader navigation={navigation} />

      <Card containerStyle={styles.card}>
        <Card.Title>Patient Profile</Card.Title>
        <Card.Divider />
        <View style={styles.infoRow}>
          <Text style={styles.label}>First Name:</Text>
          <Text style={styles.infoText}>{firstName}</Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.label}>Last Name:</Text>
          <Text style={styles.infoText}>{lastName}</Text>
        </View>
        <View style={styles.infoRow}>
          <Text style={styles.label}>Gender:</Text>
          <Text style={styles.infoText}>{gender}</Text>
        </View>
      </Card>

      <Card containerStyle={styles.card}>
        <Card.Title>Off-Bed</Card.Title>
        <Card.Divider />
        <View style={styles.switchContainer}>
          <Text>{offBed ? "Enabled" : "Disabled"}</Text>
          <Switch
            value={offBed}
            onValueChange={(value) => setOffBed(value)}
            trackColor={{ false: "gray", true: "green" }}
          />
        </View>
      </Card>

      <Card containerStyle={styles.card}>
        <Card.Title>Exit-Door</Card.Title>
        <Card.Divider />
        <View style={styles.switchContainer}>
          <Text>{exitDoor ? "Enabled" : "Disabled"}</Text>
          <Switch
            value={exitDoor}
            onValueChange={(value) => setExitDoor(value)}
            trackColor={{ false: "gray", true: "green" }}
          />
        </View>
      </Card>
    </View>
  );
};

export default PatientProfile
