// src/components/alert.js
import React from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import Modal from 'react-native-modal';

const defaultPositiveButton = {
    text: 'OK',
    backgroundColor: 'blue',
    color: 'white',
    onPress: () => { }
}

const Alert = ({ isVisible, title, body, positiveButton = defaultPositiveButton, negativeButton = undefined }) => {
    return (
        <Modal isVisible={isVisible}>
            <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
                <Text style={{ color: 'white' }}>{title}</Text>
                <Text style={{ color: 'white' }}>{body}</Text>
                <View style={{ flexDirection: 'row', marginTop: 20 }}>
                    {negativeButton && (
                        <TouchableOpacity
                            style={{
                                backgroundColor: negativeButton.backgroundColor,
                                padding: 10, borderRadius: 5, marginHorizontal: 5
                            }}
                            onPress={negativeButton.onPress}
                        >
                            <Text style={{ color: negativeButton.color || 'black' }}>{negativeButton.text}</Text>
                        </TouchableOpacity>
                    )}

                    <TouchableOpacity
                        style={{
                            backgroundColor: positiveButton.backgroundColor,
                            padding: 10, borderRadius: 5, marginHorizontal: 5
                        }}
                        onPress={positiveButton.onPress}
                    >
                        <Text style={{ color: positiveButton.color || 'white' }}>{positiveButton.text}</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </Modal>
    );
};

export default Alert;
