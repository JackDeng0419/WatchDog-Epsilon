// src/views/create-patient.js
import React, { useState } from 'react';
import { View, Text, TextInput } from 'react-native';
import { Button, Card } from '@rneui/base';
import { Picker } from '@react-native-picker/picker';

import { SUCCESS_STATUS, ERROR_STATUS, createNewPatient } from '../apis/serve-api';
import AppHeader from '../components/header';
import Alert from '../components/alert';

import { createPatientStyles as styles } from '../asset/create-patient-style';

const CreatePatient = ({ navigation }) => {
  const initialPatientDetail = {
    firstName: '',
    lastName: '',
    gender: 'MALE',
    bedId: ''
  };
  const [patientDetail, setPatientDetail] = useState(initialPatientDetail);
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
  const handleSubmit = async () => {
    let newAlertState = { ...initialAlertState };

    if (!firstName || !lastName || !gender || !bedId) {
      newAlertState = {
        ...newAlertState,
        isVisible: true,
        body: 'Please fill in all fields.',
        positiveButton: { ...newAlertState.positiveButton, backgroundColor: 'red' }
      };
    } else {
      const patientData = {
        first_name: firstName,
        last_name: lastName,
        gender,
        bed_id: parseInt(bedId),
      };

      const response = await createNewPatient(patientData);
      if (response && response.status === SUCCESS_STATUS) {
        newAlertState = {
          ...newAlertState,
          isVisible: true,
          title: SUCCESS_STATUS.toUpperCase(),
          body: 'New patient created successfully.',
          positiveButton: {
            text: 'OK',
            backgroundColor: 'blue',
            onPress: () => navigation.navigate('PatientList')
          }
        };
      } else {
        newAlertState = {
          ...newAlertState,
          isVisible: true,
          title: ERROR_STATUS.toUpperCase(),
          body: response.data.messsage,
          positiveButton: { ...newAlertState.positiveButton, backgroundColor: 'red' }
        };
      }
    }

    setAlert(newAlertState);
  };

  const { firstName, lastName, gender, bedId } = patientDetail;
  return (
    <View style={styles.container}>
      <AppHeader navigation={navigation} />
      <Card containerStyle={styles.card}>
        <Text style={styles.label}>First Name:</Text>
        <TextInput
          style={styles.input}
          value={firstName}
          onChangeText={(text) => setPatientDetail(prevState => ({ ...prevState, firstName: text }))}
        />

        <Text style={styles.label}>Last Name:</Text>
        <TextInput
          style={styles.input}
          value={lastName}
          onChangeText={(text) => setPatientDetail(prevState => ({ ...prevState, lastName: text }))}
        />

        <Text style={styles.label}>Gender:</Text>
        <Picker
          selectedValue={gender}
          onValueChange={(value) => setPatientDetail(prevState => ({ ...prevState, gender: value }))}
        >

          <Picker.Item label="Male" value="MALE" />
          <Picker.Item label="Female" value="FEMALE" />
        </Picker>

        <Text style={styles.label}>Bed ID:</Text>
        <TextInput
          style={styles.input}
          value={bedId}
          onChangeText={(text) => {
            const regex = /^[0-9\b]+$/;
            if (text === '' || regex.test(text)) {
              setPatientDetail(prevState => ({ ...prevState, bedId: text }));
            }
          }}
          keyboardType="numeric"
        />
        <Button title="Submit" onPress={handleSubmit} />

        <Alert
          isVisible={alert.isVisible}
          title={alert.title}
          body={alert.body}
          positiveButton={alert.positiveButton}
        />

      </Card>
    </View>
  );
};

export default CreatePatient;
