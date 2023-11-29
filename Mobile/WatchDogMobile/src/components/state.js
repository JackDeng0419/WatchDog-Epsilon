export const NotificationState = {
    UNDO: 'UNDO',
    IN_PROCESS: 'IN_PROCESS',
    DONE: 'DONE'
  };
  
  export const ActionType = {
    LEAVEBED: 'LEAVEBED',
    LEAVEROOM: 'LEAVEROOM'
  };
  
  export const getStateColor = (state) => {
    switch (state) {
      case NotificationState.UNDO:
        return 'red';
      case NotificationState.IN_PROCESS:
        return 'green';
      case NotificationState.DONE:
        return 'blue';
      default:
        return 'black';
    }
  };
  