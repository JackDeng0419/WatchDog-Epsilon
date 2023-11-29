// src/views/patient-list.js
import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity } from 'react-native';
import { Card } from '@rneui/base';

import { SUCCESS_STATUS, getPatientsList } from '../apis/serve-api';
import AppHeader from '../components/header';

import { patientListStyles as styles } from '../asset/patient-list-style';

const PatientList = ({ navigation }) => {

  const [patients, setPatients] = useState([]);

  useEffect(() => {
    const fetchPatients = async () => {
      const data = await getPatientsList();
      if (data && data.status === SUCCESS_STATUS) {
        setPatients(data.patients);
      }
    };

    fetchPatients();
  }, []);

  const getStatusStyle = (status) => {
    switch (status) {
      case 'enabled':
        return styles.enabled;
      case 'disabled':
        return styles.disabled;
      case 'warning':
        return styles.warning;
      default:
        return {};
    }
  };

  return (
    <View style={styles.container}>
      <AppHeader navigation={navigation} />

      <ScrollView>
        {patients.map((patient, index) => (
          <TouchableOpacity key={index} onPress={() => navigation.navigate('PatientProfile', { patientId: patient.patientId })}>
            <Card containerStyle={styles.card}>
              <Card.Title>{`${patient.first_name} ${patient.last_name}`}</Card.Title>
              <Card.Divider />

              <View style={styles.infoRow}>
                <Text style={styles.label}>Off-Bed</Text>
                <Text style={getStatusStyle(patient.offBed)}>{patient.offBed}</Text>
              </View>

              <View style={styles.infoRow}>
                <Text style={styles.label}>Exit-Door</Text>
                <Text style={getStatusStyle(patient.exitDoor)}>{patient.exitDoor}</Text>
              </View>

            </Card>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
};

export default PatientList;
