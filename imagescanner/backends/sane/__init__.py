import sane
import logging

from imagescanner.backends import base 

class ScannerManager(base.ScannerManager):
 
    def _refresh(self):
        self._devices = []
        
        sane.init()
        devices = sane.get_devices()    
        for dev in devices: 
            scanner_id = 'sane-%s' % len(self._devices)
            try:
                scanner = Scanner(scanner_id, dev[0], dev[1], dev[2], dev[3])
                self._devices.append(scanner)
            except Exception, exc:
                # XXX: Which exception should be here?
                # Logging to try to figure it out
                logging.debug(exc)
        sane.exit()

class Scanner(base.Scanner):  
    def __init__(self, scanner_id, device, manufacturer, name, description):
        self.id = scanner_id
        self.manufacturer = manufacturer
        self.name = name
        self.description = description
        self._device = device

    def __repr__(self):
        return '<%s: %s - %s>' % (self.id, self.manufacturer, self.name)
    
    def scan(self, dpi=200):
        sane.init()
        scanner = sane.open(self._device)
        image = scanner.scan()
        scanner.close()
        sane.exit()

        return image
