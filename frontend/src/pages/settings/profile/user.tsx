import { Layout } from "@/components/layout/Layout";
import { ProfileForm } from "@/components/settings/profile-form";

export default function ProfileUserPage() {
  return (
    <Layout>
      <div className="w-full max-w-7xl space-y-12">
        <div>
          <div>
            <h1 className="text-2xl font-bold mb-6">{"Profile"}</h1>
            <div className={`flex flex-col justify-center lg:flex-row`}>
              <div className="flex flex-1 flex-col justify-start py-4 ">
                <div className="w-full max-w-md sm:w-[400px]">
                  <ProfileForm />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
