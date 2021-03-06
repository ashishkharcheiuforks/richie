import * as Sentry from '@sentry/browser';

import { CommonDataProps } from 'types/commonDataProps';

const context: CommonDataProps['context'] = (window as any)
  .__richie_frontend_context__;

if (context && context.sentry_dsn) {
  Sentry.init({
    dsn: context.sentry_dsn,
    environment: context.environment,
    release: RICHIE_VERSION,
  });
  Sentry.configureScope(scope => scope.setExtra('application', 'frontend'));
}

/**
 * Generic error handler to be called whenever we need to do error reporting throughout the app.
 * Passes errors to Sentry if available, logs the error to the console otherwise.
 */
// tslint:disable:no-console
export const handle = (error: Error) => {
  if (context.sentry_dsn) {
    Sentry.captureException(error);
  } else {
    console.error(error);
  }
};
