// src/apis/oneSignal-api.js
import React, { Component } from 'react';
import { DeviceEventEmitter } from 'react-native';
import OneSignal from 'react-native-onesignal';
import axios from 'axios';

import { ONESIGNAL_APP_ID, SERVER_END_POINT } from '../config';
import Alert from '../components/alert';

export class OneSignalApi extends Component {
  constructor() {
    super();
    OneSignal.setLogLevel(6, 0);
    OneSignal.setAppId(ONESIGNAL_APP_ID);
    this.state = {
      isModalVisible: false,
      modalTitle: '',
      modalBody: '',
      modalOnPress: null,
    };
    this._init();
  }

  _init() {
    OneSignal.setNotificationWillShowInForegroundHandler(notificationReceivedEvent => {
      let notification = notificationReceivedEvent.getNotification();
      const data = notification.additionalData;
      const headings = notification.title;
      const contents = notification.body;

      notificationReceivedEvent.complete(notification);

      this._showAlert(headings, contents, () => {
        if (data && data.targetScreen) {
          DeviceEventEmitter.emit('navigateToScreen', {
            targetScreen: data.targetScreen,
            notificationId: data.notificationId,
          });
        }
      });
    });

    OneSignal.setNotificationOpenedHandler(notification => {
      const data = notification.notification.additionalData;
      if (data && data.targetScreen) {
        DeviceEventEmitter.emit('navigateToScreen', {
          targetScreen: data.targetScreen,
          notificationId: data.notificationId,
        });
      }
    });
  }

  _showAlert(headings, body, onButtonPress) {
    this.setState({
      isModalVisible: true,
      modalTitle: headings,
      modalBody: body,
      modalOnPress: onButtonPress
    });
  }

  renderModal() {
    return (
      <Alert
        isVisible={this.state.isModalVisible}
        title={this.state.modalTitle}
        body={this.state.modalBody}
        negativeButton={{
          text: 'Not processed yet',
          backgroundColor: 'grey',
          color: 'black',
          onPress: () => {
            this.setState({ isModalVisible: false });
          }
        }}
        positiveButton={{
          text: 'Go to processing',
          backgroundColor: 'red',
          color: 'white',
          onPress: () => {
            this.setState({ isModalVisible: false });
            this.state.modalOnPress();
          }
        }}
      />
    );
  }

  render() {
    return this.renderModal();
  }
}

export const sendRequestToServer = () => {
  OneSignal.getDeviceState().then(device => {
    const userId = device.userId;
    axios
      .post(SERVER_END_POINT + 'mobile/register/', JSON.stringify({ userId }), {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .catch(error => console.error(error));
  });
};
