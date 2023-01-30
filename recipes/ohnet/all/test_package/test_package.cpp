#include <iostream>
#include <vector>

#include <OpenHome/Net/Core/OhNet.h>

using namespace std;
using namespace OpenHome;
using namespace OpenHome::Net;

int main(void)
{
  InitialisationParams *initParams = InitialisationParams::Create(); 
  Environment *env = UpnpLibrary::Initialise(initParams);

  std::vector<NetworkAdapter *> *subnetList = UpnpLibrary::CreateSubnetList();
  int pos = 1;
  for (auto iter = subnetList->begin(); iter != subnetList->end(); ++iter, ++pos)
  {
    char *full_name = (*iter)->FullName();
    cout << "Found adapter #" << pos << ": " << full_name << endl;
    free(full_name);
  }

  return EXIT_SUCCESS;
}
