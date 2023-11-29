// src/components/header.js
import React from 'react';
import { TouchableOpacity } from 'react-native';
import { Header } from '@rneui/base';
import { FontAwesomeIcon } from '@fortawesome/react-native-fontawesome';
import { faBars, faUser, faHouse } from '@fortawesome/free-solid-svg-icons';

const AppHeader = ({ navigation }) => {
  const handleLeftPress = () => {
    navigation.navigate('Home');
  };
  const handleCenterPress = () => {
    navigation.navigate('Home');
  };

  const handleRightPress = () => {
    navigation.navigate('UserProfile');
  };

  return (
    <Header
      leftComponent={
        <TouchableOpacity onPress={handleLeftPress}>
          <FontAwesomeIcon
            icon={faBars}
            color="#fff"
          />
        </TouchableOpacity>
      }
      centerComponent={
        <TouchableOpacity onPress={handleCenterPress}>
          <FontAwesomeIcon
            icon={faHouse}
            color="#fff"
          />
        </TouchableOpacity>
      }
      rightComponent={
        <TouchableOpacity onPress={handleRightPress}>
          <FontAwesomeIcon
            icon={faUser}
            color="#fff"
          />
        </TouchableOpacity>
      }
    />
  );
};

export default AppHeader;
