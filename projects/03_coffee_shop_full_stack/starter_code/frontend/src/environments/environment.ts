/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'tuncerm.eu', // the auth0 domain prefix
    audience: 'udaspice', // the audience set for the auth0 app
    clientId: 'ET0Jg4SU9F6N6ljsVFOZtBDa9OYof5N3', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application.
  }
};

