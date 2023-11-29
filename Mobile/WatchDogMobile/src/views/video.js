// src/views/video.js
import React, { useState, useEffect } from 'react';
import { View, Text } from 'react-native';
import { Video } from 'expo-av'
import { SUCCESS_STATUS, getVideoById } from '../apis/serve-api';

const VideoPage = ({ route }) => {
  const { videoId } = route.params;
  const [videoUrl, setVideoUrl] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchVideo() {
      try {
        const data = await getVideoById(videoId);
        if (data && data.status === SUCCESS_STATUS) {
          setVideoUrl(data);
        } else {
          setError('Failed to fetch video.');
        }
      } catch (err) {
        setError(err.toString());
      }
    }

    fetchVideo();
  }, [videoId]);

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Displaying video with ID: {videoId}</Text>
      {videoUrl ? (
        <Video
          source={{ uri: videoUrl }}
          rate={1.0}
          volume={1.0}
          isMuted={false}
          resizeMode="cover"
          shouldPlay
          isLooping
          style={{ width: 300, height: 170 }} // Adjust according to your needs
        />
      ) : (
        <Text>{error || 'Loading video...'}</Text>
      )}
    </View>
  );
};

export default VideoPage;
